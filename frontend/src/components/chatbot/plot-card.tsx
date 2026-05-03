import { type PlotData } from '../../lib/chatbot-api'
import { ChartBarMultiple } from './bar-chart-multiple'
import { ChartLineMultiple } from './line-chart-multiple'
import { ChartPieLabelCustom } from './pie-chart-custom-label'

export const PlotCard = ({ plot }: { plot: PlotData }) => {
  if (plot.chart_type === 'bar') {
    return (
      <div className="my-4 w-full animate-in zoom-in-95 duration-300">
        <ChartBarMultiple data={plot.data} title={plot.title} description={plot.description} />
      </div>
    );
  }
  
  if (plot.chart_type === 'pie') {
    return (
      <div className="my-4 w-full animate-in zoom-in-95 duration-300">
        <ChartPieLabelCustom data={plot.data} title={plot.title} description={plot.description} />
      </div>
    );
  }

  // default to line
  return (
    <div className="my-4 w-full animate-in zoom-in-95 duration-300">
      <ChartLineMultiple data={plot.data} title={plot.title} description={plot.description} />
    </div>
  );
};
