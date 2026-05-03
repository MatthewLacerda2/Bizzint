"use client"

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

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

export interface ChartBarMultipleProps {
  data?: any[]
  title?: string
  description?: string
}

export function ChartBarMultiple({
  data = [],
  title,
  description,
}: ChartBarMultipleProps) {
  if (!data || data.length === 0) return <div>No data available</div>

  const firstItem = data[0]
  const stringKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "string"
  )
  const numberKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "number"
  )

  const xAxisKey = stringKeys.length > 0 ? stringKeys[0] : Object.keys(firstItem)[0]
  const barKeys =
    numberKeys.length > 0 ? numberKeys : Object.keys(firstItem).filter((k) => k !== xAxisKey)

  const chartConfig = {} as ChartConfig
  barKeys.forEach((key, index) => {
    chartConfig[key] = {
      label: key.charAt(0).toUpperCase() + key.slice(1),
      color: `var(--chart-${(index % 5) + 1})`,
    }
  })

  return (
    <Card>
      {(title || description) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart accessibilityLayer data={data}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey={xAxisKey}
              tickLine={false}
              tickMargin={10}
              axisLine={false}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent indicator="dashed" />}
            />
            {barKeys.map((key) => (
              <Bar
                key={key}
                dataKey={key}
                fill={`var(--color-${key})`}
                radius={4}
              />
            ))}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
