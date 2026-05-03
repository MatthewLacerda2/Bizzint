"use client"

import { CartesianGrid, Line, LineChart, XAxis } from "recharts"

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

export interface ChartLineMultipleProps {
  data?: any[]
  title?: string
  description?: string
}

export function ChartLineMultiple({
  data = [],
  title,
  description,
}: ChartLineMultipleProps) {
  if (!data || data.length === 0) return <div>No data available</div>

  const firstItem = data[0]
  const stringKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "string"
  )
  const numberKeys = Object.keys(firstItem).filter(
    (key) => typeof firstItem[key] === "number"
  )

  const xAxisKey = stringKeys.length > 0 ? stringKeys[0] : Object.keys(firstItem)[0]
  const lineKeys =
    numberKeys.length > 0 ? numberKeys : Object.keys(firstItem).filter((k) => k !== xAxisKey)

  const chartConfig = {} as ChartConfig
  lineKeys.forEach((key, index) => {
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
          <LineChart
            accessibilityLayer
            data={data}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey={xAxisKey}
              tickLine={false}
              axisLine={false}
              tickMargin={8}
            />
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            {lineKeys.map((key) => (
              <Line
                key={key}
                dataKey={key}
                type="monotone"
                stroke={`var(--color-${key})`}
                strokeWidth={2}
                dot={false}
              />
            ))}
          </LineChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
