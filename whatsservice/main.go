package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq"
	"github.com/skip2/go-qrcode"
	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	waLog "go.mau.fi/whatsmeow/util/log"
)

var client *whatsmeow.Client
var qrCodePNG []byte

type ValidationRequest struct {
	Numbers []string `json:"numbers"`
}

type ValidationResponse struct {
	PhoneNumber  string `json:"phone"`
	IsOnWhatsApp bool   `json:"is_os_whatsapp_"`
	IsBusiness   bool   `json:"is_business"`
	Name         string `json:"name,omitempty"`
}

func setupWhatsmeow(dbURI string) {
	dbLog := waLog.Stdout("Database", "DEBUG", true)
	container, err := sqlstore.New(context.Background(), "postgres", dbURI, dbLog)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	deviceStore, err := container.GetFirstDevice(context.Background())
	if err != nil {
		log.Fatalf("Failed to get device store: %v", err)
	}

	clientLog := waLog.Stdout("Client", "DEBUG", true)
	client = whatsmeow.NewClient(deviceStore, clientLog)

	if client.Store.ID == nil {
		// No ID stored, new login
		qrChan, _ := client.GetQRChannel(context.Background())
		err = client.Connect()
		if err != nil {
			log.Fatalf("Failed to connect client: %v", err)
		}
		go func() {
			for evt := range qrChan {
				if evt.Event == "code" {
					png, err := qrcode.Encode(evt.Code, qrcode.Medium, 256)
					if err == nil {
						qrCodePNG = png
					}
				} else if evt.Event == "success" {
					qrCodePNG = nil
				}
			}
		}()
	} else {
		// Already logged in, just connect
		err = client.Connect()
		if err != nil {
			log.Fatalf("Failed to connect client: %v", err)
		}
	}
}

func main() {
	// Load .env from parent directory
	err := godotenv.Load("../.env")
	if err != nil {
		log.Println("Error loading ../.env file, using environment variables")
	}

	dbURI := os.Getenv("DATABASE_URL")
	if dbURI != "" {
		// Replace postgresql:// with postgres:// and remove +asyncpg or other driver suffixes
		dbURI = strings.Replace(dbURI, "postgresql://", "postgres://", 1)
		dbURI = strings.Replace(dbURI, "+asyncpg", "", 1)
	} else {
		dbUser := os.Getenv("POSTGRES_USER")
		dbPass := os.Getenv("POSTGRES_PASSWORD")
		dbHost := os.Getenv("POSTGRES_SERVER")
		dbPort := os.Getenv("POSTGRES_PORT")
		dbName := os.Getenv("POSTGRES_DB")

		// e.g., postgres://postgres:postgres@192.168.0.55:5434/bizzint?sslmode=disable
		dbURI = fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable", dbUser, dbPass, dbHost, dbPort, dbName)
	}

	setupWhatsmeow(dbURI)

	app := fiber.New()

	app.Get("/", func(c *fiber.Ctx) error {
		if client != nil && client.IsConnected() && client.IsLoggedIn() {
			return c.SendString("connection established")
		}
		if qrCodePNG != nil {
			c.Set("Content-Type", "image/png")
			return c.Send(qrCodePNG)
		}
		return c.SendString("Initializing or not ready")
	})

	app.Post("/validate-bunch", func(c *fiber.Ctx) error {
		if client == nil || !client.IsConnected() || !client.IsLoggedIn() {
			return c.Status(503).JSON(fiber.Map{"error": "WhatsApp client not ready"})
		}

		var req ValidationRequest
		if err := c.BodyParser(&req); err != nil {
			return c.Status(400).JSON(fiber.Map{"error": "Invalid request"})
		}

		onWA, err := client.IsOnWhatsApp(context.Background(), req.Numbers)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": "Failed to check numbers"})
		}

		var results []ValidationResponse
		var jidsToFetch []types.JID
		jidMap := make(map[types.JID]int)

		for i, item := range onWA {
			res := ValidationResponse{
				PhoneNumber:  item.Query,
				IsOnWhatsApp: item.IsIn,
			}
			results = append(results, res)

			if item.IsIn {
				jidsToFetch = append(jidsToFetch, item.JID)
				jidMap[item.JID] = i
			}
		}

		if len(jidsToFetch) > 0 {
			infoMap, err := client.GetUserInfo(context.Background(), jidsToFetch)
			if err == nil {
				for jid, info := range infoMap {
					idx := jidMap[jid]

					if info.VerifiedName != nil {
						results[idx].Name = info.VerifiedName.Details.GetVerifiedName()
					}
					if results[idx].Name == "" {
						results[idx].Name = info.Status
					}

					results[idx].IsBusiness = info.VerifiedName != nil
				}
			}
		}

		// return in the format { phone_numbers: { phone, is_os_whatsapp_, is_business }} Wait, the prompt says:
		// { phone_numbers: { phone, is_os_whatsapp_, is_business }} - actually it means a list or object mapping phone numbers. 
		// I'll format as {"phone_numbers": results} but I'll fix the struct tags.
		
		return c.JSON(fiber.Map{
			"phone_numbers": results,
		})
	})

	log.Fatal(app.Listen(":3000"))
}
