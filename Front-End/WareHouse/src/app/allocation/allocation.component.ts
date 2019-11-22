import { Component, OnInit } from '@angular/core';
import { FilesServiceService } from '../Service/files-service.service';
import { FileSystemFileEntry, NgxFileDropEntry, FileSystemDirectoryEntry } from 'ngx-file-drop';
import { saveAs } from 'file-saver';
import { Racks } from '../Clases/Racks';
import { Rack } from '../Clases/Rack';

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
  selector: 'app-allocation',
  templateUrl: './allocation.component.html',
  styleUrls: ['./allocation.component.css']
})
export class AllocationComponent implements OnInit {

  constructor(  private http: FilesServiceService ) { }
  // Variables de la paginación pageActual: numero de pagina; itemsPorPagina: su nombre lo dice
  pageActual = 1;
  itemsPorPagina = 1;
  pageActual2 = 1;
  itemsPorPagina2 = 10;

  // Variables Archivo de entrada
  public FileNameAlloc: string;
  public ExcelFileAlloc: File;
  public filesArrayAlloc: File[] = [];
  public fileDownAlloc = undefined;

  // Variables servicio Rack
  public receivedRacks: Racks;
  public llegoServicio = false;
  public receivedRacksPrint: Racks = {fo: 0, racks: []};
  public receivedRacksRefPrint: [number, number][] = [];
  public nr: Rack;

  // Variables Data section
  public tmlimitAlloc: any;
  public valueTmlimitAlloc: number;
  public disablePopover = false;

  // Variables del filtro1 y filtro2
  public busqueda: any;
  public filterValue: any = undefined;
  public busquedaRef: any;
  public filterValueRef: any = undefined;
  public verifica: boolean; // Variable por utilizar


  // =================== Input File Button =======================
  public inputFileAlloc(file: File) {
    this.ExcelFileAlloc = file[0];
    this.FileNameAlloc = file[0].name;
    console.log(this.ExcelFileAlloc);
    this.filesArrayAlloc[0] = this.ExcelFileAlloc;
  }
  // ==============================================================

  // ======================== Input File Drag and Drop ================================
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
  sendDataAlloc(tl: any) {
    let decisor1 = false;
    let decisor2 = false;
    if ( this.filesArrayAlloc[0] ) { decisor1 = true; } else { decisor1 = false; }
    if ( tl === undefined || tl === null ||  tl <= 0 ) { decisor2 = false; } else { decisor2 = true; }

    console.log(decisor1);
    console.log(decisor2);
    this.valueTmlimitAlloc = Number(tl);

    if ( decisor1 === true && decisor2 === true ) {
      this.disablePopover = true;
      this.servicePostFilesAlloc();
    } else {
      this.disablePopover = false;
    }
  }
  // =====================================================================================================

  // =================== Send Data: Excel File. Receive: File Results and JSON ============================
  public errorService: boolean = false;
  servicePostFilesAlloc() {
    if (this.filesArrayAlloc[0]) {
      this.http.postFilesAllocation(this.filesArrayAlloc, this.valueTmlimitAlloc).subscribe(

        response => {
          console.log(response);
          this.convertBLOBtoXLSX(response);
          this.errorService = false;
        },

        ( error: any ) => { 
          console.log('Error en el servicio'); 
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
  convertBLOBtoXLSX( data: any ) {
    this.fileDownAlloc = new Blob([data], {
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
    console.log(this.fileDownAlloc);
  }
  // ===============================================================================

  // ================== Function Download Results File =======================
  downloadFileAlloc() {
    if (this.llegoServicio === true) {
      saveAs(this.fileDownAlloc, 'Resultados_Asignacion' + '.xlsx');
    }
  }
  // ==========================================================================

  // ================== Service GET data Results in JSON ========================
  serviceDataJSON() {
    this.http.getRacks().subscribe(

      (data: Racks) => { this.receivedRacks = data; },

      error => { console.log(error); },

      () => {
        console.log(this.receivedRacks);
        this.getRackstoPrint();
      }

    );
  }
  // =============================================================================

  // ==================== Convert data receives in aveilable to print ==========================
  getRackstoPrint() {
    this.receivedRacksPrint.fo = this.receivedRacks.fo;
    for ( const rack of this.receivedRacks.racks ) {
      if ( rack.referencias.length > 0 ) {
        this.nr = Object.assign({}, rack); // Object.assign: like th copy in python
        if ( this.nr.hileras === true ) {
          this.nr.hileras = 'Si';
        } else {
          this.nr.hileras = 'No';
        }
        this.receivedRacksPrint.racks.push(this.nr);
      }
    }
    console.log('.');
    console.log(this.receivedRacksPrint);
    this.getRacksRefPrint();
  }
  // ==============================================================================================

  // ======================== Convert data to second option print =================================
  getRacksRefPrint() {
    for ( const rack of this.receivedRacksPrint.racks ) {
      for ( const ref of rack.referencias ) {
        this.receivedRacksRefPrint.push([Number(ref), Number(rack.id)]);
      }
    }

    let aux: [number, number];
    for ( let i = 0; i < this.receivedRacksRefPrint.length; i++ ) {
      for ( let j = i; j < this.receivedRacksRefPrint.length; j++ ) {
        if ( this.receivedRacksRefPrint[i][0] > this.receivedRacksRefPrint[j][0] ) {
          aux = this.receivedRacksRefPrint[i];
          this.receivedRacksRefPrint[i] = this.receivedRacksRefPrint[j];
          this.receivedRacksRefPrint[j] = aux;
        }
      }
    }
  }
  // ==============================================================================================

  // =============================== Function Filter 1 ===================================
  buscarRef(receivedFilterRef: any) {
    console.log(receivedFilterRef);
    if ( receivedFilterRef === undefined ) {
      this.filterValueRef = undefined;
    } else if ( receivedFilterRef === null ) {
      this.filterValueRef = null;
    } else {
      this.filterValueRef = Number(receivedFilterRef); // parseInt(numero, base)
    }
  }
  // ======================================================================================


  // ======================================= Function Filter 2 ================================
  buscarRack(receivedFilter: any) {
    console.log(receivedFilter);
    if ( receivedFilter === undefined ) {
      this.filterValue = undefined;
    } else if ( receivedFilter === null ) {
      this.filterValue = null;
    } else {
      this.filterValue = Number(receivedFilter); // parseInt(numero, base)

      // Si el rack quedó con referencias
      this.verifica = false;
      if ( this.receivedRacks.racks[this.filterValue - 1].referencias.length > 0 ) {
        this.verifica = true;
      }
    }
  }
  // ===========================================================================================

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
