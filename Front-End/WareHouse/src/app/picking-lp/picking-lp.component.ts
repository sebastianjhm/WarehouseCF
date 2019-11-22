import { Component, OnInit } from '@angular/core';
import { NgxFileDropEntry, FileSystemFileEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';

import { saveAs } from 'file-saver';
import { Rutas } from '../Clases/Rutas';
import { FilesServiceService } from '../Service/files-service.service';

interface Alert {
  type: string;
  message: string;
}

const ALERTS: Alert[] = [
  {
    type: 'secondary',
    message: 'This is a secondary alert',
  }
];

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

  // Variables Data section
  public tmlimitPicking: any;
  public valueTmlimitPicking: number;
  public disablePopover = false;

  // =================== Input File Button =======================
  public inputFile(file: File) {
    this.ExcelFilePicking = file[0];
    this.FileNamePicking = file[0].name;
    console.log(this.ExcelFilePicking);
    this.filesArrayPicking[0] = this.ExcelFilePicking;
  }
  // ==============================================================

  // ======================== Input File Drag and Drop ================================
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
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
      }
    }
  }

  public fileOver(event: any) {
    console.log(event);
  }

  public fileLeave(event: any) {
    console.log(event);
  }
  // ==================================================================================

  // ================================ Data Section: Function Send Data ==================================
  sendDataPicking(tl: any) {
    console.log(Number(tl));
    let decisor1 = false;
    let decisor2 = false;
    if (this.filesArrayPicking[0]) { decisor1 = true; } else { decisor1 = false; }
    if ( tl === undefined || tl === null ||  tl <= 0 ) { decisor2 = false; } else { decisor2 = true; }

    console.log(decisor1);
    console.log(decisor2);
    this.valueTmlimitPicking = Number(tl);

    if ( decisor1 === true && decisor2 === true ) {
      this.disablePopover = true;
      this.servicePostFilesPicking();
    } else {
      this.disablePopover = false;
    }
  }
  // =====================================================================================================

  // =================== Send Data: Excel File. Receive: File Results and JSON ============================
  public errorService: boolean = false;
  servicePostFilesPicking() {
    if (this.filesArrayPicking[0]) {
      this.http.postFilesPicking(this.filesArrayPicking, this.valueTmlimitPicking).subscribe(

        response => {
          console.log(response);
          this.convertBLOBtoXLSX(response);
          this.errorService = false;
        },

        error => {
          console.log(error);
          this.errorService = true;
          this.reset();
        },

        () => {
          this.serviceDataJSON();
          this.llegoServicio = true;
          (document.getElementById('button-download') as HTMLInputElement).disabled = false;
        }

      );
    }
  }
  // ======================================================================================================

  // ================= Convert Blob received in service in XLSX ====================
  convertBLOBtoXLSX(data: any) {
    this.fileDownPicking = new Blob([data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    console.log(this.fileDownPicking);
  }
  // ===============================================================================

  // ================== Function Download Results File =======================
  downloadFilePicking() {
    if (this.llegoServicio === true) {
      saveAs(this.fileDownPicking, 'Resultados_Picking' + '.xlsx');
    }
  }
  // ==========================================================================

  // ================== Service GET data Results in JSON ========================
  serviceDataJSON() {
    this.http.getRuta().subscribe(

      (data: Rutas) => { this.receivedRuta = data; },

      error => { console.log(error); },

      () => { console.log(this.receivedRuta); }

    );
  }
  // =============================================================================

  // ======================== Initial Function: Property TypeScript ==========================
  ngOnInit() {
    this.serviceDataJSON();
    (document.getElementById('button-download') as HTMLInputElement).disabled = true;
  }
  // =========================================================================================


  alerts: Alert[];
  close(alert: any) {
    this.alerts.splice(this.alerts.indexOf(alert), 1);
  }

  reset() {
    this.alerts = Array.from(ALERTS);
  }
}
