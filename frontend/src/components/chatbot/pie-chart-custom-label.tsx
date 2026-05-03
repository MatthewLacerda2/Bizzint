"use client"

import { Pie, PieChart } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart"

export interface ChartPieLabelCustomProps {
  data?: any[]
  title?: string
  description?: string
}

export function ChartPieLabelCustom({
  data = [],
  title,
  description,
}: ChartPieLabelCustomProps) {
  if (!data || data.length === 0) return <div>No data available</div>

  const firstItem = data[0]
  const stringKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "string"
  )
  const numberKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "number"
  )

  const nameKey = stringKeys.length > 0 ? stringKeys[0] : Object.keys(firstItem)[0]
  const dataKey =
    numberKeys.length > 0 ? numberKeys[0] : Object.keys(firstItem).filter((k) => k !== nameKey)[0]

  const chartConfig = {
    [dataKey]: { label: dataKey.charAt(0).toUpperCase() + dataKey.slice(1) },
  } as ChartConfig

  const processedData = data.map((item, index) => {
    const originalName = String(item[nameKey])
    const safeKey =
      originalName.toLowerCase().replace(/[^a-z0-9]/g, "_") || `key_${index}`

    chartConfig[safeKey] = {
      label: originalName,
      color: `var(--chart-${(index % 5) + 1})`,
    }

    return {
      ...item,
      [nameKey]: safeKey,
      fill: `var(--color-${safeKey})`,
    }
  })

  return (
    <Card className="flex flex-col">
      {(title || description) && (
        <CardHeader className="items-center pb-0">
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px] px-0"
        >
          <PieChart>
            <ChartTooltip
              content={<ChartTooltipContent nameKey={nameKey} hideLabel />}
            />
            <Pie
              data={processedData}
              dataKey={dataKey}
              labelLine={false}
              label={({ payload, ...props }) => {
                return (
                  <text
                    cx={props.cx}
                    cy={props.cy}
                    x={props.x}
                    y={props.y}
                    textAnchor={props.textAnchor}
                    dominantBaseline={props.dominantBaseline}
                    fill="var(--foreground)"
                  >
                    {payload[dataKey]}
                  </text>
                )
              }}
              nameKey={nameKey}
            />
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
