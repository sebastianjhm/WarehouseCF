import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Rutas } from '../Clases/Rutas';
import { Racks } from '../Clases/Racks';

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
    return this.http.post(this.url + '/postFilePicking' , sendFormDataPicking, {responseType: 'arraybuffer'});
  }

  getRuta() {
    console.log('Trayendo Data Picking');
    console.log(this.url + '/rutas');
    return this.http.get<Rutas>(this.url + '/rutas');
  }

  postFilesAllocation( ReceivedFileAllocation: File[] ) {
    console.log('Send file allocation');
    const sendFormDataAllocation = new FormData();
    sendFormDataAllocation.append('myExcelFileAlloc', ReceivedFileAllocation[0]);
    return this.http.post(this.url + '/postFileAllocation' , sendFormDataAllocation, {responseType: 'arraybuffer'});
  }

  getRacks() {
    console.log('trayendo Data Allocation');
    console.log(this.url + '/racks');
    return this.http.get<Racks>(this.url + '/racks');
  }

}
