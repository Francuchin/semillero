import { Component,ViewChild, OnInit, ViewChildren } from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import { AnalisisService } from './services/analisis.service';
import { CanvasMuestraComponent } from './components/canvas-muestra/canvas-muestra.component'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'semillero-cliente';
  image=null;

  @ViewChild(CanvasMuestraComponent,{static:false})canvas: CanvasMuestraComponent;
  constructor(private anal:AnalisisService){
  }

  ngOnInit(){ 
  }

  analizamesta(){
    fetch(this.image)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], 'imagen.jpg', blob)
      let maxw=this.canvas.imageBounds.getNorthEast().lng
      let maxh=this.canvas.imageBounds.getNorthEast().lat
      let w = this.canvas.muestraBounds.getSouthWest().lng
      let h = maxh-this.canvas.muestraBounds.getSouthWest().lat
      let x = this.canvas.muestraBounds.getNorthEast().lng
      let y = maxh-this.canvas.muestraBounds.getNorthEast().lat

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
          this.canvas.removerMuestra();
          let seguras = res.seguras
          let inseguras = res.inseguras
          for(let result of seguras){
            this.canvas.dibujarRectangulo(result, maxh, false)
          }
          for(let result of inseguras){
            this.canvas.dibujarRectangulo(result, maxh,true)
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
      img.onload= () => this.canvas.loadImage(img);
    }
    reader.onerror = function (error) {
     console.log('Error: ', error);
    };
  }

}
