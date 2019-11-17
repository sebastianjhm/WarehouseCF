import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgxFileDropModule } from 'ngx-file-drop';
import { HttpClientModule } from '@angular/common/http';
import { NgxPaginationModule } from 'ngx-pagination';
import { PickingLPComponent } from './picking-lp/picking-lp.component';
import { AllocationComponent } from './allocation/allocation.component';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    PickingLPComponent,
    AllocationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxFileDropModule,
    HttpClientModule,
    NgxPaginationModule,
    FormsModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
