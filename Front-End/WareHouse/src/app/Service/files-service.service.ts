import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Rutas } from "../Clases/Rutas";

@Injectable({
  providedIn: 'root'
})
export class FilesServiceService {

  constructor( private http: HttpClient ) { }

  url = 'http://localhost:5000';

  postFiles(ReceivedFile: File[]) {
    console.log('ahí lo envié');

    const sendFormData = new FormData();
    sendFormData.append('myExcelFile', ReceivedFile[0]);
    return this.http.post(this.url + '/postFile' , sendFormData, {responseType: 'arraybuffer'});
  }

  getRuta() {
    console.log("Estoy trayendo el json");
    console.log(this.url + '/rutas')
    return this.http.get<Rutas>(this.url + '/rutas')
  }
}
