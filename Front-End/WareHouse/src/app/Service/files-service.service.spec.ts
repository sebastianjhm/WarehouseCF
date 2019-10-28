import { TestBed } from '@angular/core/testing';

import { FilesServiceService } from './files-service.service';

describe('FilesServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FilesServiceService = TestBed.get(FilesServiceService);
    expect(service).toBeTruthy();
  });
});
