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

  postFilesPicking( ReceivedFilePicking: File[], tmlimit: number) {
    console.log('Service: Send file picking');
    const sendFormDataPicking = new FormData();
    sendFormDataPicking.append('myExcelFile', ReceivedFilePicking[0]);
    sendFormDataPicking.append('timeLimit', String(tmlimit));
    return this.http.post(this.url + '/postFilePicking' , sendFormDataPicking, {responseType: 'arraybuffer'});
  }

  getRuta() {
    console.log('Service: Trayendo Data Picking');
    console.log(this.url + '/rutas');
    return this.http.get<Rutas>(this.url + '/rutas');
  }

  getResultsPicking() {
    console.log(this.url + '/resultsPicking');
    return this.http.get(this.url + '/resultsPicking', {responseType: 'arraybuffer'});
  }

  postFilesAllocation( ReceivedFileAllocation: File[], tmlimit: number  ) {
    console.log('Service: Send file allocation');
    const sendFormDataAllocation = new FormData();
    sendFormDataAllocation.append('myExcelFileAlloc', ReceivedFileAllocation[0]);
    sendFormDataAllocation.append('timeLimit', String(tmlimit));
    return this.http.post(this.url + '/postFileAllocation' , sendFormDataAllocation, {responseType: 'arraybuffer'});
  }

  getRacks() {
    console.log('Service: trayendo Data Allocation');
    console.log(this.url + '/racks');
    return this.http.get<Racks>(this.url + '/racks');
  }

  getResultsAllocation() {
    console.log(this.url + '/resultsAllocation');
    return this.http.get(this.url + '/resultsAllocation', {responseType: 'arraybuffer'});
  }

}
