import { Component, OnInit } from '@angular/core';
import { FilesServiceService } from '../Service/files-service.service';
import { FileSystemFileEntry, NgxFileDropEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';
import { saveAs } from 'file-saver';
import { Racks } from '../Clases/Racks';
import { Rack } from '../Clases/Rack';

@Component({
  selector: 'app-allocation',
  templateUrl: './allocation.component.html',
  styleUrls: ['./allocation.component.css']
})
export class AllocationComponent implements OnInit {

  constructor(  private http: FilesServiceService ) { }
  // Variables de la paginación pageActual: numero de pagina; itemsPorPagina: su nombre lo dice
  pageActual = 1;
  itemsPorPagina = 1;

  // Variables Archivo de entrada
  public FileNameAlloc: string;
  public ExcelFileAlloc: File;
  public filesArrayAlloc: File[] = [];
  public fileDownAlloc = undefined;

  // Variables servicio Rack
  public receivedRacks: Racks;
  public llegoServicio = false;
  public receivedRacksPrint: Racks = {fo: 0, racks: []};
  public nr: Rack;

  public inputFileAlloc(file: File) {
    this.ExcelFileAlloc = file[0];
    this.FileNameAlloc = file[0].name;
    console.log(this.ExcelFileAlloc);
    this.filesArrayAlloc[0] = this.ExcelFileAlloc;
    this.sendFilesAlloc();
  }

  public droppedFileAlloc(files: NgxFileDropEntry[]) {
    console.log('dropped');
    console.log(files);
    for (const droppedFile of files) {
      // Si es un archivo
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          // Here you can access the real file
          this.ExcelFileAlloc = file;
          this.FileNameAlloc = this.ExcelFileAlloc.name;
          this.filesArrayAlloc[0] = this.ExcelFileAlloc;
          this.sendFilesAlloc();
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }

  sendFilesAlloc() {
    console.log('Lo recibí');
    if (this.filesArrayAlloc[0]) {
      this.http.postFilesAllocation(this.filesArrayAlloc).subscribe(

        response => {
          console.log(response);
          this.convertBLOBtoXLSX(response);
        },

        ( error: any ) => { console.log('Error en el servicio'); console.log(error); },

        () => {
          this.getTablaAllocation();
          (document.getElementById('button-download') as HTMLInputElement).disabled = false;
          this.llegoServicio = true;
        }

      );
    }
  }

  convertBLOBtoXLSX( data: any ) {
    this.fileDownAlloc = new Blob([data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    console.log(this.fileDownAlloc);
  }

  downloadFileAlloc() {
    if (this.llegoServicio === true) {
      saveAs(this.fileDownAlloc, 'Resultados_Asignacion' + '.xlsx');
    }
  }

  getTablaAllocation() {
    this.http.getRacks().subscribe(

      (data: Racks) => { this.receivedRacks = data; },

      error => { console.log(error); },

      () => {
        console.log(this.receivedRacks);
        this.getRackstoPrint();
      }

    );
  }

  getRackstoPrint() {
    this.receivedRacksPrint.fo = this.receivedRacks.fo;
    for ( const rack of this.receivedRacks.racks ) {
      if ( rack.referencias.length > 0 ) {
        this.nr = Object.assign({}, rack); // Object.assign: like th copy in python
        if ( this.nr.hileras === true) {
          this.nr.hileras = 'Si';
        } else {
          this.nr.hileras = 'No';
        }
        this.receivedRacksPrint.racks.push(this.nr);
      }
    }
    console.log('.');
    console.log(this.receivedRacksPrint);
  }

  public fileOver(event: any) {
    console.log(event);
  }

  public fileLeave(event: any) {
    console.log(event);
  }

  ngOnInit() {
    this.getTablaAllocation();
    (document.getElementById('button-download') as HTMLInputElement).disabled = true;
  }

}
