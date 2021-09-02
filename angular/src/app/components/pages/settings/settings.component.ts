import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { SocketIoService } from '../../../services/socketio.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {

  public settingsForm = this.formBuilder.group({
    radaar: this.formBuilder.group({
	    api_key: ['', Validators.required],
    }),
    sonaar: this.formBuilder.group({
	    api_key: ['', Validators.required],
    }),
  });

  constructor(
    private formBuilder: FormBuilder,
    private socketIoService: SocketIoService,
  ) { }

  ngOnInit(): void { }

  onSubmit(): void {
    this.socketIoService.updateSettings(this.settingsForm.value);
  }

}
