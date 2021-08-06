import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MoviesComponent }   from './components/pages/movies/movies.component';
import { TvShowsComponent }  from './components/pages/tv-shows/tv-shows.component';
import { FilesComponent }    from './components/pages/files/files.component';
import { SettingsComponent } from './components/pages/settings/settings.component';

const routes: Routes = [
  { path: 'movies', component: MoviesComponent },
  { path: 'tv-shows', component: TvShowsComponent },
  { path: 'files', component: FilesComponent },
  { path: 'settings', component: SettingsComponent },
  { path: '',   redirectTo: '/movies', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
