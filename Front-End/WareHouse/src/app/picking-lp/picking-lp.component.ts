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

  constructor( private http: FilesServiceService ) {}
  // Variables de la paginación pageActual: numero de pagina; itemsPorPagina: su nombre lo dice
  pageActual = 1;
  itemsPorPagina = 1;

  // Variables Archivo
  public FileNamePicking: string;
  public ExcelFilePicking: File;
  public filesArrayPicking: File[] = [];
  public fileDownPicking = undefined;

  // Variables del servicio Ruta
  public receivedRuta: Rutas;
  public llegoServicio = false;

  public inputFile(file: File) {
    this.ExcelFilePicking = file[0];
    this.FileNamePicking = file[0].name;
    console.log(this.ExcelFilePicking);
    this.filesArrayPicking[0] = this.ExcelFilePicking;
    this.sendFiles();
  }

  public droppedFile(files: NgxFileDropEntry[]) {
    console.log('dropped');
    console.log(files);
    for (const droppedFile of files) {
      // Si es un archivo
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          // Here you can access the real file
          this.ExcelFilePicking = file;
          this.FileNamePicking = this.ExcelFilePicking.name;
          this.filesArrayPicking[0] = this.ExcelFilePicking;
          this.sendFiles();
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }

  sendFiles() {
    if (this.filesArrayPicking[0]) {
      this.http.postFilesPicking(this.filesArrayPicking).subscribe(

        response => {
          console.log(response);
          this.convertBLOBtoXLSX(response);
        },

        error => { console.log(error); },

        () => {
          this.getTablaPicking();
          this.llegoServicio = true;
          (document.getElementById('button-download') as HTMLInputElement).disabled = false;
        }

      );
    }
  }

  convertBLOBtoXLSX(data: any) {
    this.fileDownPicking = new Blob([data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    console.log(this.fileDownPicking);
  }


  getTablaPicking() {
    this.http.getRuta().subscribe(

      (data: Rutas) => { this.receivedRuta = data; },

      error => { console.log(error); },

      () => { console.log(this.receivedRuta); }

    );
  }

  downloadFile() {
    if (this.llegoServicio === true) {
      saveAs(this.fileDownPicking, 'Resultados_Picking' + '.xlsx');
    }
  }

  public fileOver(event: any) {
    console.log(event);
  }

  public fileLeave(event: any) {
    console.log(event);
  }

  ngOnInit() {
    this.getTablaPicking();
    (document.getElementById('button-download') as HTMLInputElement).disabled = true;
  }

}
