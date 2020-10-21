// date-time.service
import { Injectable } from '@angular/core';
import * as moment from 'moment';

@Injectable({ providedIn: 'root' })
export class DateTimeService
{
  public getFormat(): string
  {
    return "MM/DD/YYYY"; // format for users
  }
  public getLocale(): string
  {
    return "us-EN"; // add you own logic here
  }  
}
