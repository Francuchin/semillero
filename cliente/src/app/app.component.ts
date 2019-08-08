import { Component,ViewChild, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'semillero-cliente';
  @ViewChild('layout',{static:false}) canvasRef;
  image =null;
  constructor(){
  }
  ngOnInit(){ 
  }
  inputFile($event){
		var reader = new FileReader();
		reader.readAsDataURL($event.target.files[0]);
		reader.onload =  () =>{
		  	this.image = new Image();
		  	this.image.src =reader.result;
		}
		reader.onerror = function (error) {
		 console.log('Error: ', error);
		};
  }

}
