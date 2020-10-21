import { Component, OnInit } from '@angular/core';  
import { UniquePicturesService } from '../unique-pictures.service';
import { takeUntil } from 'rxjs/operators'
import { MatDatepickerInputEvent } from '@angular/material/datepicker'
//import { MatNativeDateModule } from '@angular/material/core';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import * as moment from "moment";

@Component({  
	selector: 'app-home',  
	templateUrl: './home.component.html',  
	styleUrls: ['./home.component.css']  
})

export class HomeComponent implements OnInit {
  epoch : Date = new Date(1970,0,1); // good value for our corpus
  start_date : Date = this.epoch;
  end_date : Date = new Date(2034,0,1);
  pictures = [];

	constructor(private uniquePicturesService: UniquePicturesService) { }
	ngOnInit() {
    this.callUrl(this.uniquePicturesService.make_range(this.start_date, this.end_date)
      + "&" + this.uniquePicturesService.default_filter);
  }

  // make a start time/end time control and if either is changed
  // do the right callUrl?
  public dateChange(type, event: MatDatepickerInputEvent<MatMomentDateModule>) {
    console.log("in dateChange: " + this.start_date + ' ' + this.end_date)
    this.callUrl(this.uniquePicturesService.make_range(this.start_date, this.end_date)
      + "&" + this.uniquePicturesService.default_filter);
  }
  
  public callUrl(url) {
    this.pictures = [];
    this.uniquePicturesService.sendGetRequestToUrl(url)
      .subscribe((data: any[]) => {
        this.pictures = data;
      })
  }

  
  public toggleTag(picture, event) {  
    var label = '#' + event.target.innerText + ', ';
    if (-1 != picture[4].indexOf(label)) {
      picture[4] = picture[4].replace(label,'')
    }
    else {
      picture[4] += label;
    }
    // TODO persist the change!
    this.uniquePicturesService.sendPatchToUrl(picture[0] + " " + picture[1] + " " + picture[2], picture[4])
      .subscribe((data: any[]) => {
        console.log(data);
        // TODO reload the curent page to filter out by filter changes?
      })
  }

  // TODO implement filtering by tag and datetime range
  // set not_before date from date picker
  // set not_after date from date picker
  // set filter from filter radio control

  public firstPage() {
    return this.callUrl(this.uniquePicturesService.first)
  }
  public lastPage() {
    return this.callUrl(this.uniquePicturesService.last)
  }
  public beforePage() {
    return this.callUrl(this.uniquePicturesService.before)
  }
  public afterPage() {
    return this.callUrl(this.uniquePicturesService.after)
  }
} 
