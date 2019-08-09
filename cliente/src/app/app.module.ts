import { BrowserModule } from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'; 
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CanvasMuestraComponent } from './components/canvas-muestra/canvas-muestra.component';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { AnalisisService } from './services/analisis.service'
@NgModule({
  declarations: [
    AppComponent,
    CanvasMuestraComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    LeafletModule,
    AppRoutingModule
  ],
  providers: [AnalisisService],
  bootstrap: [AppComponent]
})
export class AppModule { }
