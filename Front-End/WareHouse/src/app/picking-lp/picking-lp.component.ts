import { Component, OnInit } from '@angular/core';
import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';

import { saveAs } from 'file-saver';
import { Rutas } from '../Clases/Rutas';
import { FilesServiceService } from '../Service/files-service.service';


@Component({
  selector: 'app-picking-lp',
  templateUrl: './picking-lp.component.html',
  styleUrls: ['./picking-lp.component.css']
})
export class PickingLPComponent implements OnInit {

  constructor( private http:FilesServiceService ) {}
  // Variables de la paginación pageActual: numero de pagina; itemsPorPagina: su nombre lo dice
  pageActual = 1;
  itemsPorPagina = 1;
  
  // Variables Archivo
  FileName: string;
  public ExcelFile: File;
  public filesArray: File[] = [];
  public fileD = undefined;
  public llegoServicio = false;

  // Variables Ruta
  public receivedRuta: Rutas;

  public clickVector(file: File) {
    this.ExcelFile = file[0];
    this.FileName = file[0].name;
    console.log(this.ExcelFile);
    this.filesArray[0] = this.ExcelFile;
    this.sendFiles();
  }

  public droppedVector(files: NgxFileDropEntry[]) {
    console.log('dropped');
    console.log(files);
    for (const droppedFile of files) {
      // Si es un archivo
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          // Here you can access the real file
          // console.log(droppedFile.relativePath, file);
          this.ExcelFile = file;
          this.FileName = this.ExcelFile.name;
          this.filesArray[0] = this.ExcelFile;
          this.sendFiles();
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }

  sendFiles() {

    if (this.filesArray[0]) {
      this.http.postFiles(this.filesArray).subscribe(
        res => {
          console.log(res);
          (<HTMLInputElement> document.getElementById("b")).disabled = false;
          this.convertBLOBtoXLSX(res);
        },
        err => {
          console.log(err);
        }
      );
    }
  }

  convertBLOBtoXLSX(data: any) {
    this.fileD = new Blob([data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    console.log(this.fileD);
    this.llegoServicio = true;

    // Invocar JSON de ruta
    this.getTabla();
  }


  getTabla() {
    this.http.getRuta().subscribe((data: Rutas) => {
      this.receivedRuta = data;
    });
    setTimeout(() => {
      console.log(this.receivedRuta);
    }, 2000);
    
  }


  downloadFile() {
    if (this.llegoServicio === true) {
      saveAs(this.fileD, 'Results' + '.xlsx');
    }
  }

  public fileOver(event: any) {
    console.log(event);
  }

  public fileLeave(event: any) {
    console.log(event);
  }

  sleep(time: number) {
    return new Promise((resolve) => setTimeout(resolve, time));
  }

  ngOnInit(){
    (<HTMLInputElement> document.getElementById("b")).disabled = true;
  }

}
