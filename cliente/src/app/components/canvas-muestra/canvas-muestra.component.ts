import { Component, AfterViewInit, ViewChild, ElementRef, Input, Output, EventEmitter } from '@angular/core';
import { latLng, 
    tileLayer,
    Bounds,
    LatLngBounds,
    layerGroup,
    ImageOverlay,
    imageOverlay,
    marker,
    control,
    icon,
    circle,
    rectangle,
    Rectangle,
    divIcon,
    polygon,
    Poligon,
    LayerGroup,
    Marker,
    Map,
    Control,
    DomUtil,
    LatLng,
    CRS,
    Circle} from 'leaflet';
function convexHull(points) {
  points.sort(function (a, b) {
      return a.x != b.x ? a.x - b.x : a.y - b.y;
  });

  var n = points.length;
  var hull = [];

  for (var i = 0; i < 2 * n; i++) {
      var j = i < n ? i : 2 * n - 1 - i;
      while (hull.length >= 2 && removeMiddle(hull[hull.length - 2], hull[hull.length - 1], points[j]))
          hull.pop();
      hull.push(points[j]);
  }

  hull.pop();
  return hull;
}

function removeMiddle(a, b, c) {
  var cross = (a.x - b.x) * (c.y - b.y) - (a.y - b.y) * (c.x - b.x);
  var dot = (a.x - b.x) * (c.x - b.x) + (a.y - b.y) * (c.y - b.y);
  return cross < 0 || cross == 0 && dot <= 0;
}
class Recuadro {
  public map:Map;
  public cantidad:number;
  public correccion:number;
  public maxh:number;
  public color:string;
  public result:any;
  public rectangulo:Rectangle;     
      
  showConvexHull() {  
    var latlngArray = [];
    let x = this.maxh-this.result.bbox[0]
    let y = parseInt(this.result.bbox[1])
    let convex:boolean[][] = this.result.convex_image
    let huul = convex.map((c,i)=>c.map((r,j)=>{
      if(!r) return false;
      return {
        x:x - convex.length + i,
        y:y + c.length - j
      }
    }).filter(col=>!!col)).filter(coors=>!!coors.filter(coor=>!!coor).length).reduce((prev,next)=>prev.concat(next))
    //console.log(huul)
      var points = latlngArray.map(element=> { 
          return {
              x: element.lat,
              y: element.lng
            }
          })
      var convexHullPoints = convexHull(huul);
      //console.log(convexHullPoints)
      var leafletHull = convexHullPoints.map(element=>([element.x,element.y]))
      return polygon(leafletHull,{color:'#FF0000'}).addTo( this.map);     
      
  }


  constructor(map:Map, result:any, maxh:number) {
    this.map=map;
    this.result = result;
    this.maxh = maxh;
    this.cantidad = result.cantidad;
    this.correccion = result.cantidad;
    this.dibujarRectangulo();
  }
  public dibujarRectangulo(){// result.centroid, result.convex_image
    let bb = this.result.bbox
    let p1:any = [this.maxh-bb[0],bb[1]]
    let p2:any = [this.maxh-bb[2],bb[3]]
    let resB = new LatLngBounds([p1,p2])
    let cantidad = parseInt(this.result.cantidad)
    this.color = cantidad<.5?"#0000ff30": cantidad>1.8?"#ff000080": "#00ff0050"
    this.rectangulo = rectangle(resB, {color: this.color, weight: 1}).addTo(this.map)
  }
  public centrar(){
    let rec = this.result.bbox;
    let fit = new LatLngBounds([
      [this.maxh-rec[0]+15, rec[1]-15],
      [this.maxh-rec[2]-15, rec[3]+15]
    ])
    this.map.fitBounds(fit);
    this.rectangulo.setStyle({color:'#00000000'})
    return rectangle(fit, {color: "#FF000050", weight: 2}).addTo(this.map)
  }
  public mostrar = () =>this.rectangulo.setStyle({color:this.color})
}


@Component({
  selector: 'app-canvas-muestra',
  templateUrl: './canvas-muestra.component.html',
  styleUrls: ['./canvas-muestra.component.scss']
})
export class CanvasMuestraComponent implements AfterViewInit {
  public map:Map;
  public group:any;
  public imageoverlay:ImageOverlay;
  public zoom:number = 15;
  image=null
  public imageBounds = new LatLngBounds([[0,0], [500,700]]);
  public muestraBounds = new LatLngBounds([[0,0], [500,700]]);
  puntouno=null;
  public 
  public muestra:Rectangle=null
  public hull:Poligon=null
  actual=0;
  resultados:Recuadro[]=[];
  ngAfterViewInit(){

  }
  public maxh=0;
  public loadImage(img){
    this.imageBounds = new LatLngBounds([[0,0],[img.height,img.width]])
    let fit = new LatLngBounds([[-img.height,-img.width],[img.height,img.width]])
    this.map.setMaxBounds(this.imageBounds);
    this.map.fitBounds(fit);
    if(this.map.hasLayer(this.imageoverlay))
      this.map.removeLayer(this.imageoverlay)
    this.imageoverlay = imageOverlay(img.src,this.imageBounds).addTo(this.map);
  }
  public corregirSiguiente(){
    this.removerMuestra();
    if(this.resultados.length > this.actual){
      let actual = this.resultados[this.actual];
      if(actual)
        actual.mostrar();
    }
    this.actual=this.resultados.length>this.actual?this.actual+1:0;
    if(this.resultados.length > this.actual){
      let actual = this.resultados[this.actual];
      if(actual) {
        this.muestra = actual.centrar()
        this.hull = actual.showConvexHull()
      }
    }
  }
  public removerMuestra(){
    if(this.map.hasLayer(this.muestra))
      this.map.removeLayer(this.muestra)
    if(this.map.hasLayer(this.hull))
      this.map.removeLayer(this.hull)
  }
  /*

  esto tiene que ser mas inteligente 
  tipo crear objetos que tengan estados y eso por cada cuadro con semilla encontrado
  que permitan su correccion y posterior aprendisaje

  */

  public dibujarRectangulo(result, maxh, color){// result.centroid, result.convex_image
    this.maxh = maxh
    this.resultados.push(new Recuadro(this.map,result,maxh))
  }

  click= $event=>{
    console.log($event)
    let x = $event.latlng.lng
    let y = $event.latlng.lat
    if(!this.puntouno)
      this.puntouno = [y,x]
    else{
      this.muestraBounds = new LatLngBounds([[y,x], this.puntouno])
      if(this.map.hasLayer(this.muestra))
        this.map.removeLayer(this.muestra)
      this.muestra = rectangle(this.muestraBounds, {color: "#ff7800", weight: 1}).addTo(this.map)
      this.puntouno = null
    }
  }
  leafletMapReady(map: Map) {
    if(!map && !this.map) return;
    this.map=map;
    var maxBounds = new LatLngBounds([[-500,-700], [500,700]]);
    this.map.options.crs = CRS.Simple;
    this.map.setZoom(1)
    this.map.setMinZoom(.1)
    this.map.setMaxBounds(this.imageBounds);
    this.map.fitBounds(maxBounds);
    this.map.on("zoomend", e=> { this.zoom = e.target.getZoom() });
    this.map.on("click",this.click);
    //this.group = layerGroup().addTo(this.map);
    if(!this.image) return;
    this.imageoverlay = imageOverlay(this.image,this.imageBounds).addTo(this.map);
  }
}
var EPSILON_LOW =  0.003;
var EPSILON =      0.00001;
var EPSILON_HIGH = 0.00000001;

function epsilonEqual(a, b, epsilon){
  if(epsilon === undefined){ epsilon = EPSILON_HIGH; }
  return ( Math.abs(a - b) < epsilon );
}

function arrayContainsObject(array, object) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] === object) {
            return true;
        }
    }
    return false;
}

// points should be an array of objects {x:___, y:___} where ___ values should be numbers
function convexHull2(points){
  // validate input
  if(points === undefined || points.length === 0){ return []; }
  // # points in the convex hull before escaping function
  var INFINITE_LOOP = 10000;
  // sort points by x and y
  var sorted = points.sort(function(a,b){
      if(a.x-b.x < -EPSILON_HIGH){ return -1; }
      if(a.x-b.x > EPSILON_HIGH){ return 1; }
      if(a.y-b.y < -EPSILON_HIGH){ return -1; }
      if(a.y-b.y > EPSILON_HIGH){ return 1; }
      return 0;});
  var hull = [];
  hull.push(sorted[0]);
  // the current direction the perimeter walker is facing
  var ang = 0;  
  var infiniteLoop = 0;
  do{
    infiniteLoop++;
    var h = hull.length-1;
    var angles = sorted
      // remove all points in the same location from this search
      .filter(function(el){ 
        return !(epsilonEqual(el.x, hull[h].x, EPSILON_HIGH) && epsilonEqual(el.y, hull[h].y, EPSILON_HIGH)) })
      // sort by angle, setting lowest values next to "ang"
      .map(function(el){
        var angle = Math.atan2(hull[h].y - el.y, hull[h].x - el.x);
        while(angle < ang){ angle += Math.PI*2; }
        return {node:el, angle:angle}; })
      .sort(function(a,b){return (a.angle < b.angle)?-1:(a.angle > b.angle)?1:0});
    if(angles.length === 0){ return []; }
    // narrowest-most right turn
    var rightTurn = angles[0];
    // collect all other points that are collinear along the same ray
    angles = angles.filter(function(el){ return epsilonEqual(rightTurn.angle, el.angle, EPSILON_LOW); })
    // sort collinear points by their distances from the connecting point
    .map(function(el){ 
      var distance = Math.sqrt(Math.pow(hull[h].x-el.node.x, 2) + Math.pow(hull[h].y-el.node.y, 2));
      el.distance = distance;
      return el;})
    // (OPTION 1) exclude all collinear points along the hull 
    .sort(function(a,b){return (a.distance < b.distance)?1:(a.distance > b.distance)?-1:0});
    // (OPTION 2) include all collinear points along the hull
    // .sort(function(a,b){return (a.distance < b.distance)?-1:(a.distance > b.distance)?1:0});
    // if the point is already in the convex hull, we've made a loop. we're done
    if(arrayContainsObject(hull, angles[0].node)){ return hull; }
    // add point to hull, prepare to loop again
    hull.push(angles[0].node);
    // update walking direction with the angle to the new point
    ang = Math.atan2( hull[h].y - angles[0].node.y, hull[h].x - angles[0].node.x);
  }while(infiniteLoop < INFINITE_LOOP);
  return [];
}