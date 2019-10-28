import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PickingLPComponent } from './picking-lp.component';

describe('PickingLPComponent', () => {
  let component: PickingLPComponent;
  let fixture: ComponentFixture<PickingLPComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PickingLPComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PickingLPComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
