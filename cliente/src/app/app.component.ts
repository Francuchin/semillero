import { Component,ViewChild, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  title = 'semillero-cliente';
  @ViewChild('layout',{static:false}) canvasRef;
  imgUrl = null;
  constructor(){
  }
  ngOnInit(){
  }
  inputFile($event){
		var reader = new FileReader();
		reader.readAsDataURL($event.target.files[0]);
		reader.onload =  () =>{
	  	this.imgUrl = reader.result
	  	setTimeout(()=>this.drawRectangle({
	  		left:50,
	  		top:50,
	  		width:50,
	  		height:50
	  	}),50)
		}
		reader.onerror = function (error) {
		 console.log('Error: ', error);
		};
  }

	drawRectangle(file: any): void
	{
	    let canvas = this.canvasRef.nativeElement;
	    let context = canvas.getContext('2d');

	    let source = new Image();
	    source.src = this.imgUrl;

	    source.onload = (e) =>
	    {
	    		console.log(context)
	        context.drawImage(source,0,0);
	        context.beginPath();
	        context.rect(file.left, file.top, file.width, file.height);
	        context.stroke();  
	    };


	}
}
