import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';

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

}
