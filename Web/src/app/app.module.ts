import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { ContentBlockComponent } from './content_block/content_block.component';
import { HeaderMenuComponent } from './header_menu/header_menu.component';


@NgModule({
  declarations: [
    AppComponent,
    HeaderMenuComponent,
    ContentBlockComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
