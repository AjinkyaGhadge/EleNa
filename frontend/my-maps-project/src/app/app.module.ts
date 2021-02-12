import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AgmCoreModule } from '@agm/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
// import { DirectionsMapDirective } from './directions-map.directive';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from '@angular/material/slider';
import {MatToolbarModule} from '@angular/material/toolbar';
import {FormsModule} from '@angular/forms';
import {MatRadioModule} from '@angular/material/radio';
import {AgmDirectionModule} from 'agm-direction';
import {MatGridListModule} from '@angular/material/grid-list';
import { HttpClientModule } from '@angular/common/http';
import {MatButtonModule} from '@angular/material/button'

@NgModule({
  declarations: [
    AppComponent,
    // DirectionsMapDirective
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    MatSliderModule,
    MatRadioModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyANBJfk8OsDGMa7QBR6IIzc2uJn3EqYslo'
    }),
    BrowserAnimationsModule,
    MatToolbarModule,
    AgmDirectionModule,
    MatGridListModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
