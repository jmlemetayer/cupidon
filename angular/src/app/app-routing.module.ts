import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { FilesComponent } from './files/files.component';

const routes: Routes = [
  { path: 'files', component: FilesComponent },
  { path: '',   redirectTo: '/files', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
