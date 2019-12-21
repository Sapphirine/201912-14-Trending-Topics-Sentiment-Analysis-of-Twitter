import React from "react";

class LocMarker extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loc: props.loc,
      isHover: props.chosen
    };
  }
  componentDidUpdate() {
    console.log("DidUpdate...");
    this.state.isHover = this.props.chosen;
  }
  color = () => {
    if (!this.state.isHover) {
      return '#E91E63';
    } else {
      return '#a2e91e';
    }
  }

  toggleHover = () => {
    console.log("hover change...");
    const val = (this.state.isHover)? false:true;
    this.setState({
      loc: this.state.loc,
      isHover: val
    });
    console.log(this.state.isHover);
    if (!this.state.isHover) {
      console.log("update loc...");
      this.props.updateWindow(this.props.loc, this.props.name, {});
    } else {
      console.log("reset...");
      this.props.updateWindow([], "", {});
    }
    console.log(this.state.isHover);
  }

  toggleClick = () => {
    console.log("click change...");
    const val = (this.state.isHover)? false:true;
    console.log(this.props.name + " is " + (val? "chosen":"unchosen"));
    console.log("now " + this.props.name + " is " + (this.state.isHover? "chosen":"unchosen"));
    if (val===true) {
      console.log("update loc...");
      this.props.updateWindow(this.props.loc, this.props.name, {});
    } else {
      console.log("reset...");
      this.props.updateWindow([], "", {});
    }
  }

  info = () => {
    console.log("return infoPad...");
    const styles = {position: 'absolute', backgroundColor: 'black', width: 100, height: 100, top: 0, left: 0};
      return (
        <div style={styles}>
        </div>
      );
  }

  render() {
    return (
          <g className="markers">
            {}
            <circle
            cx={ this.state.loc[0] }
            cy={ this.state.loc[1] }
            r={ 10 }
            fill={this.props.color}
            className="marker"
            onClick={this.toggleClick}
            />
          </g>
    );
  }
}

export { LocMarker }
