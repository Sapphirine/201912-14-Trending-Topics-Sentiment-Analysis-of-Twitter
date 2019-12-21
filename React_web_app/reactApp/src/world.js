import React from "react";
import { geoEqualEarth, geoPath } from "d3-geo";
import { feature } from "topojson-client";
import { locations } from "./locations.js";
import { LocMarker } from "./locMarker.js";
import { InfoPad, ChartPad } from "./infoPane.js";
import "konva/lib/shapes/Rect";
import "konva/lib/shapes/Text";
import "konva/lib/shapes/Circle";
import "konva/lib/shapes/Line";
import { PGraph } from "./Pgraph.js";

const viewX = 1200;
const viewY = 675;
const updatePeriod = 10 * 1000;
let apiUrl = 'https://hw1-jl5255.appspot.com/';
apiUrl = 'http://localhost:5000'


const projection = geoEqualEarth()
  .scale(viewX/5)
  .translate([ viewX / 2, viewY / 2 ]);


class WorldClass extends React.Component {
  constructor(props) {
    super(props);
    let chosen = {};
    let i = 0;
    for (i=0; i<locations.length; ++i) {
      chosen[locations[i].name] = false;
    }
    this.state = {
      geographies: [],
      chosen: chosen,
      infoWindow: {
        loc: [],
        name: "",
      },
      data: {},
      isPaneOpen: false
    };
    /*
    Loading world map data
    */
    fetch("/world-110m.json")
      .then(response => {
        if (response.status !== 200) {
          console.log(`There was a problem: ${response.status}`)
        }
        response.json().then(worlddata => {
          this.setState({
            geographies: (feature(worlddata, worlddata.objects.countries).features),
            chosen: this.state.chosen,
            infoWindow: this.state.infoWindow,
            data: this.state.data,
            isPaneOpen: this.state.isPaneOpen
          });
        })
      });
    /*
    Fetching the initial location/topic data
    */
    try {
      console.log("trying...");
      fetch(apiUrl, {mode: 'cors', credentials: 'same-origin'})
        .then(response => {
          if (response.status !== 200) {
            console.log("failed...");
            console.log(response);
          }
          response.json().then(fetched => {
            console.log(fetched);
            this.state.data = fetched;
          })
        });
    } catch (error) {
      console.log(error);
    }
  }

  componentDidMount() {
    /*fetch("http://localhost:5000/search", {
      method: 'POST',
      body: JSON.stringify({'text': "test echo..."})
    }).then(response => {
      console.log(response);
      if (response.status !== 200) {
        console.log("failed echo...");
      }
      response.json().then(data => {
        console.log(data);
      })
    })*/
    this.timer = setInterval(() => {
      try {
        console.log("trying...");
        fetch(apiUrl, {mode: 'cors', credentials: 'same-origin'})
          .then(response => {
            if (response.status !== 200) {
              console.log("failed...");
              console.log(response);
            }
            console.log(response);
            response.json().then(fetched => {
              console.log(fetched);
              const copy = {...this.state};
              copy.data = fetched;
              this.setState(copy);
            })
          });
      } catch (error) {
        console.log(error);
      }
    }, updatePeriod);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  updateWindow = (loc, name, data) => {
    console.log("showing " + name + "...");
    const copy = {...this.state};
    for (const p in copy.chosen) {
      copy.chosen[p] = false;
    }
    if (name !== "") {
      copy.chosen[name] = true;
    }
    copy.infoWindow.loc = loc;
    copy.infoWindow.name = name;
    copy.infoWindow.data = data;
    this.setState(copy);
  }

  renderWindow = () => {
    if (this.state.infoWindow.name!=="") {
      const styles = {
        position: 'absolute',
        top: this.state.infoWindow.loc[1] + 32,
        left: this.state.infoWindow.loc[0] + 12,
        backgroundColor: '#f5f2e9'
      };
      console.log("return info...");
      const name = this.state.infoWindow.name;
      let data = this.state.data.plainData[name];
      if (!data) {
        data = [{'topic': 'No Data', 'sentiment': [0, 0.5, -0.5]}];
      }
      return (
        <div style={styles}>
          <p>{name}</p>
          <InfoPad data={data}/>
        </div>
      );
    } else {
      console.log("return none...");
      return null;
    }
  }
  
  renderChart(styles, data) {
    console.log(this.state.isPaneOpen);
    if (this.state.isPaneOpen) {
      let styles2 = {...styles};
      styles2.left = styles.left + 500;
      styles2.height = 500;
      styles2.width = 500;
      styles2.backgroundColor = '#000000';
      return (
          <div className={"ChartBlocker"} style={styles}>
            <PGraph
              id={"graph"}
              data={data}
            />
          </div>
      );
    } else {
      return null;
    }
  }

  chartButton = () => {
    let copy = {...this.state};
    const open = this.state.isPaneOpen? false : true;
    copy.isPaneOpen = open;
    this.setState(copy);
  }

  render() {
    return (
        <div style={{position: 'relative'}}>
          <div style={{ marginTop: '32px', top: 10, left: 10, width:150 }}>
            <button onClick={ this.chartButton }>
            ......
            </button>
          </div>
          <svg width={ viewX } 
              height={ viewY } 
              viewBox={"0 0 ".concat(viewX.toString(10), " ", viewY.toString(10))}
              >
              <g className="countries">
                {
                  this.state.geographies.map((d,i) => (
                    <path
                    key={ `path-${ i }` }
                    d={ geoPath().projection(projection)(d) }
                    className="country"
                    fill={ `rgba(38,50,56,${ 1 / this.state.geographies.length * i})` }
                    stroke="#FFFFFF"
                    strokeWidth={ 0.5 }
                    />
                  ))
                }
              </g>
              { locations.map((pt) => (
                <LocMarker 
                updateWindow={this.updateWindow} 
                loc={projection(pt.geo)} 
                color={this.state.chosen[pt.name]? '#A2E91E':'#E91E63' }
                name={pt.name}
                chosen={this.state.chosen[pt.name]}
                /> )) }
          </svg>
          { this.renderWindow()}
          { this.renderChart(
            {
              position: 'absolute',
              top: 675,
              left: 5,
              height: 500,
              width: 500,
              backgroundColor: '#f8f8f0'
          }, this.state.data.locGraph) }
          { this.renderChart(
            {
              position: 'absolute',
              top: 675,
              left: 510,
              height: 500,
              width: 500,
              backgroundColor: '#f8f8f0'
            }, this.state.data.topGraph) }
        </div>
        )
      }
  }

export { WorldClass }
