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
    LayerGroup,
    Marker,
    Map,
    Control,
    DomUtil,
    LatLng,
    CRS,
    Circle} from 'leaflet';
    
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
  public muestra:Rectangle=null

  ngAfterViewInit(){

  }

  public loadImage(img){
    this.imageBounds = new LatLngBounds([[0,0],[img.height,img.width]])
    let fit = new LatLngBounds([[-img.height,-img.width],[img.height,img.width]])
    this.map.setMaxBounds(this.imageBounds);
    this.map.fitBounds(fit);
    if(this.map.hasLayer(this.imageoverlay))
      this.map.removeLayer(this.imageoverlay)
    this.imageoverlay = imageOverlay(img.src,this.imageBounds).addTo(this.map);
  }

  /*

  esto tiene que ser mas inteligente 
  tipo crear objetos que tengan estados y eso por cada cuadro con semilla encontrado
  que permitan su correccion y posterior aprendisaje

  */

  public dibujarRectangulo(result, maxh, color){// result.centroid, result.convex_image
    let bb = result.bbox
    let p1:any = [maxh-bb[0],bb[1]]
    let p2:any = [maxh-bb[2],bb[3]]
    let resB = new LatLngBounds([p1,p2])
    rectangle(resB, {color: color, weight: 1}).addTo(this.map)
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