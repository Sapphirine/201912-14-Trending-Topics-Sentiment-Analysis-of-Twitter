import React from "react";
import { Graph } from 'react-d3-graph';


const myConfig = {
  nodeHighlightBehavior: true,
  linkLength: 50,
  d3: {
    gravity: -51,
  },
  height: 500,
  width: 500,
  node: {
    highlightStrokeColor: 'blue'
  },
  link: {
    highlightColor: 'lightblue'
  }
};

class PGraph extends React.Component {
  render() {
    return (
      <Graph
        id={this.props.id}
        data={this.props.data}
        config={myConfig}
      />
    );
  }
}

export { PGraph }
