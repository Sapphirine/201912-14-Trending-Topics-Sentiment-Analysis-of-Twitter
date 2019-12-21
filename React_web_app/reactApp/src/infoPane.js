import React from "react";
import { FixedSizeList as List } from "react-window";
import './padStyle.css';
import { PGraph } from "./Pgraph.js";

const left = 6;
const width = 108;
const top = 20;
const height = 5;
const posColor = "#9ad67e";
const negColor = "#d93016";


const data = {
  nodes: [
    {id: 'Harry'},
    {id: 'Sally'},
    {id: 'Alice'}
  ],
  links: [
    {source: 'Harry', target: 'Sally'},
    {source: 'Harry', target: 'Alice'},
  ]
};



const Chart = props => {
  const {data, index, style} = props;
  return (
    <div className={index%2 === 0? "RowEven":"RowOdd"} style={style}>
      <PGraph 
        id={"test1"}
        data={data}
      />
    </div>
  );
}

const Row = props => {
  const { data, index, style } = props;
  let pos = data[index].sentiment[1];
  let neg = -data[index].sentiment[2];
  if (pos===0 && neg===0) {
    pos = 0.5;
    neg = 0.5;
  }
  const posWidth = (pos/(pos+neg)) * width;
  const negWidth = width - posWidth;

  const style1 = {position: 'absolute', left: left, top: 20, width: posWidth, height: 5, backgroundColor: posColor };
  const style2 = {position: 'absolute', left: left+posWidth, top: 20, width: negWidth, height: 5, backgroundColor: negColor};
  const style3 = {position: 'absolute', top: 5};

  return (
    <div className={index % 2 === 0 ? "RowEven" : "RowOdd"} style={style}>
      <div style={style3}>{data[index].topic}</div>
      <div style={style1}></div>
      <div style={style2}></div>
    </div>
  )
};
 
class InfoPad extends React.Component {
  render() {
    const count = this.props.data.length;
    const height = (count*35>150)? 150:count*35;
    return (
      <List
        height={height}
        itemCount={count}
        itemSize={35}
        width={120}
        itemData={this.props.data}
      >
        {Row}
      </List>
    );
  }
}


class ChartPad extends React.Component {
  render() {
    return (
      <List
        height={this.props.size}
        itemCount={1}
        itemSize={this.props.size}
        width={this.props.size}
        itemData={this.props.data}
      >
        {Chart}
      </List>
    );
  }
}

export { InfoPad, ChartPad }
