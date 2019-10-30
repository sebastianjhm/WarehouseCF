import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PickingLPComponent } from './picking-lp/picking-lp.component';
import { AllocationComponent } from './allocation/allocation.component';


const routes: Routes = [
  { path: 'pick', component: PickingLPComponent },
  { path: 'alloc', component: AllocationComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
