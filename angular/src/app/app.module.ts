import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';

import { FlexLayoutModule }   from '@angular/flex-layout';
import { MatButtonModule }    from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule }      from '@angular/material/icon';
import { MatInputModule }     from '@angular/material/input';
import { MatListModule }      from '@angular/material/list';
import { MatSidenavModule }   from '@angular/material/sidenav';
import { MatToolbarModule }   from '@angular/material/toolbar';

import { AppRoutingModule }  from './app-routing.module';
import { RootComponent }     from './components/root/root.component';
import { PageComponent }     from './components/core/page/page.component';
import { MoviesComponent }   from './components/pages/movies/movies.component';
import { TvShowsComponent }  from './components/pages/tv-shows/tv-shows.component';
import { FilesComponent }    from './components/pages/files/files.component';
import { SettingsComponent } from './components/pages/settings/settings.component';

const socketIoConfig: SocketIoConfig = {url: window.location.origin, options: {}};

@NgModule({
  declarations: [
    RootComponent,
    PageComponent,
    MoviesComponent,
    TvShowsComponent,
    FilesComponent,
    SettingsComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    SocketIoModule.forRoot(socketIoConfig),
    FlexLayoutModule,
    MatButtonModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatSidenavModule,
    MatToolbarModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [RootComponent]
})
export class AppModule { }
