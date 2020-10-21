import { TestBed } from '@angular/core/testing';

import { UniquePicturesService } from './unique-pictures.service';

describe('UniquePicturesService', () => {
  let service: UniquePicturesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UniquePicturesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
