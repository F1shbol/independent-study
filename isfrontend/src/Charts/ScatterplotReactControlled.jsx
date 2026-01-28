import * as d3 from 'd3';
import Card from '../UI/Card';
import ChartContainer from '../ChartComponents/ChartContainer';
import Circle from '../ChartComponents/Circle';
import Axis from '../ChartComponents/Axis';

const ScatterplotReactControlled = props => {
  const width = 550;
  const height = 500;
  const innerWidth = width - props.margin.left - props.margin.right;
  const innerHeight = height - props.margin.top - props.margin.bottom;

  // I guess the domain is the extent of the data, and the range is the render size
  const xScale = d3.scaleLinear()
    // .domain([0, d3.max(props.data, d => d.user_count)])
    .domain([0, d3.max(props.data, d => d.playcount)])
    .range([0, innerWidth])
    .nice();
  const yScale = d3.scaleLinear()
    // .domain([0, 100])
    .domain([0, d3.max(props.data, d => d.x1w)])
    .range([innerHeight, 0]);

  return (
    <Card>
      <h2>Chart name</h2>
      <ChartContainer
        width={width}
        height={height}
        margin={props.margin}
      >
        <Axis 
          type="bottom"
          scale={xScale}
          innerWidth={innerWidth}
          innerHeight={innerHeight}
          label={"Playcount"}
        />
        <Axis 
          type="left"
          scale={yScale}
          innerWidth={innerWidth}
          innerHeight={innerHeight}
          label={"Listeners (1w)"}
        />
        {props.data.map(framework => (
          <Circle 
            // key={`circle-${framework.id}`}
            // cx={xScale(framework.user_count)}
            // cy={yScale(framework.retention_percentage)}
            key={`circle-${framework.name}`}
            cx={xScale(framework.playcount)}
            cy={yScale(framework.x1w)}
            r={6}
            // fill={props.colorScale(framework.id)}
          />
        ))}
      </ChartContainer> 
    </Card>
  )
};

export default ScatterplotReactControlled;