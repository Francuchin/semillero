import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, tap } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AnalisisService {
	private apiUrl = 'http://localhost:8080'
  constructor(private httpClient: HttpClient) { }
  analizar(imagen, x,y,w,h): Observable<any> {
  	const formData = new FormData();
		formData.append('file', imagen);
		formData.append('x',x);
		formData.append('y',y);
		formData.append('w',w);
		formData.append('h',h);
    return this.httpClient.post<any>(`${this.apiUrl}`, formData)
  }
}
