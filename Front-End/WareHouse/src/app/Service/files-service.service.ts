import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Rutas } from '../Clases/Rutas';

@Injectable({
  providedIn: 'root'
})
export class FilesServiceService {

  constructor( private http: HttpClient ) { }

  url = 'http://localhost:5000';

  postFilesPicking( ReceivedFilePicking: File[] ) {
    console.log('Send file picking');
    const sendFormDataPicking = new FormData();
    sendFormDataPicking.append('myExcelFile', ReceivedFilePicking[0]);
    return this.http.post(this.url + '/postFile' , sendFormDataPicking, {responseType: 'arraybuffer'});
  }

  postFilesAllocation( ReceivedFile: File[] ) {
    console.log('Send file allocation');
  }

  getRuta() {
    console.log('Estoy trayendo el json');
    console.log(this.url + '/rutas');
    return this.http.get<Rutas>(this.url + '/rutas');
  }
}
