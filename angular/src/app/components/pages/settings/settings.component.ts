import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Subscription } from 'rxjs';

import { SocketIoService } from '../../../services/socketio.service';
import { Settings } from '../../../models/settings.model';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit, OnDestroy {

  public settingsForm = this.formBuilder.group({
    radarr: this.formBuilder.group({
      url: ['', Validators.required],
      api_key: ['', Validators.required],
    }),
    sonarr: this.formBuilder.group({
      url: ['', Validators.required],
      api_key: ['', Validators.required],
    }),
  });

  private subscription: Subscription = new Subscription();

  constructor(
    private formBuilder: FormBuilder,
    private socketIoService: SocketIoService,
  ) { }

  ngOnInit(): void {
    this.socketIoService.readSettings((settings: Settings) => {
      this.settingsForm.setValue(settings);
    });

    this.subscription = this.socketIoService.onSettingsUpdated().subscribe((settings: Settings) => {
      this.settingsForm.setValue(settings);
    });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  onSubmit(): void {
    this.socketIoService.updateSettings(this.settingsForm.value);
  }

}
