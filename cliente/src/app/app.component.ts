import { Component,ViewChild, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
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
import { AnalisisService } from './services/analisis.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'semillero-cliente';
  public map:Map;
  public group:any;
  public imageoverlay:ImageOverlay;
  public zoom:number = 15;
  image=null
  imageBounds = new LatLngBounds([[0,0], [500,700]]);
  muestraBounds = new LatLngBounds([[0,0], [500,700]]);
  puntouno=null;
  public muestra:Rectangle=null
  constructor(private anal:AnalisisService){
  }
  ngOnInit(){ 
  }
  public leafletMapReady(map: Map) {
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
  analizamesta(){
    fetch(this.image)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], 'imagen.jpg', blob)
      let maxw=this.imageBounds.getNorthEast().lng
      let maxh=this.imageBounds.getNorthEast().lat

      let w = this.muestraBounds.getSouthWest().lng
      let h = maxh-this.muestraBounds.getSouthWest().lat
      let x = this.muestraBounds.getNorthEast().lng
      let y = maxh-this.muestraBounds.getNorthEast().lat

      if(w>x){
        let _w = w;
        w=x;
        x=_w
      }
      if(h>y){
        let _h = h;
        h=y;
        y=_h 
      }
      this.anal.analizar(file,
        Math.round(w),
        Math.round(h), 
        Math.round(x),
        Math.round(y),
        ).subscribe(res=>{
          let seguras = res.seguras
          let inseguras = res.inseguras
          for(let result of seguras){
            let bb = result.bbox
            let p1:any = [maxh-bb[0],bb[1]]
            let p2:any = [maxh-bb[2],bb[3]]
            let resB = new LatLngBounds([p1,p2])
            rectangle(resB, {color: "#55ff55", weight: 1}).addTo(this.map)
          }
          for(let result of inseguras){
            let bb = result.bbox
            let p1:any = [maxh-bb[0],bb[1]]
            let p2:any = [maxh-bb[2],bb[3]]
            let resB = new LatLngBounds([p1,p2])
            rectangle(resB, {color: "#ff5555", weight: 1}).addTo(this.map)
          }
        })      
    })
  }
  inputFile($event){
    var reader = new FileReader();
    if($event.target.files && $event.target.files.length)
      reader.readAsDataURL($event.target.files[0]);
    reader.onload =  (e:any) =>{
      let img = new Image()
      img.src = e.target.result
      this.image = e.target.result
      img.onload= () =>{
        this.imageBounds = new LatLngBounds([[0,0],[img.height,img.width]])
        let fit = new LatLngBounds([[-img.height,-img.width],[img.height,img.width]])
        this.map.setMaxBounds(this.imageBounds);
        this.map.fitBounds(fit);
        if(this.map.hasLayer(this.imageoverlay))
          this.map.removeLayer(this.imageoverlay)
        this.imageoverlay = imageOverlay(img.src,this.imageBounds).addTo(this.map);
      }
    }
    reader.onerror = function (error) {
     console.log('Error: ', error);
    };
  }


}
