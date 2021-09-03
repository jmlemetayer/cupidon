import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

import { Movie } from '../models/movie.model';
import { Settings } from '../models/settings.model';

@Injectable({
  providedIn: 'root'
})
export class SocketIoService {

  constructor(private socket: Socket) { }

  updateSettings(settings: Settings): void {
    this.socket.emit('settings:update', settings);
  }

  readSettings(acknowledge: (settings: Settings) => void): void {
    this.socket.emit('settings:read', acknowledge);
  }

  onSettingsUpdated(): Observable<Settings> {
    return this.socket.fromEvent<Settings>('settings:updated');
  }

  readMovies(acknowledge: (movies: Movie[]) => void): void {
    this.socket.emit('movies:read', acknowledge);
  }

}
