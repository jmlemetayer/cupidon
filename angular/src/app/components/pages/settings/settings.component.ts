import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  settingsForm = this.fb.group({
    radaarApiKey: null,
    sonaarApiKey: null,
  });

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
  }

  onSubmit(): void {
    alert("Submitted");
  }
}
