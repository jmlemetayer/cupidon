import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';

import { Settings } from '../models/settings.model';

@Injectable({
  providedIn: 'root'
})
export class SocketIoService {

  constructor(private socket: Socket) { }

  updateSettings(settings: Settings): void {
    this.socket.emit('settings:update', settings);
  }

}
