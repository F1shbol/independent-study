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

  const roundedLog = Math.ceil(Math.log2(d3.max(props.data, d => d.x1w)))
  const paddedMax = Math.pow(2,roundedLog)

  console.log("roudned log", roundedLog);
  console.log("padded max", paddedMax);

  const xScale = d3.scaleLinear()
    // .domain([0, d3.max(props.data, d => d.user_count)])
    .domain([0, d3.max(props.data, d => d.playcount)])
    .range([0, innerWidth])
    .nice();
  // const yScale = d3.scaleLinear()
  //   // .domain([0, 100])
  //   .domain([0, d3.max(props.data, d => d.x1w)])
  //   .range([innerHeight, 0]);
  // const yScale = d3.scaleLog([d3.min(props.data, d => d.x1w), d3.max(props.data, d => d.x1w)], [innerHeight, 0])
  const yScale = d3.scaleLog([d3.min(props.data, d => d.x1w), paddedMax+1], [innerHeight, 0])
      .base(2)
      .nice();

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
          <g key={`point-${framework.name}`}>
            <Circle
              cx={xScale(framework.playcount)}
              cy={yScale(framework.x1w)}
              r={3}
              // fill={props.colorScale(framework.id)}
            />
            <text
              x={xScale(framework.playcount)}
              y={yScale(framework.x1w) - 8}
              textAnchor="middle"
              fontSize="9"
              fill="#333"
            >
              {framework.name}
            </text>
          </g>
        ))}
      </ChartContainer> 
    </Card>
  )
};

export default ScatterplotReactControlled;