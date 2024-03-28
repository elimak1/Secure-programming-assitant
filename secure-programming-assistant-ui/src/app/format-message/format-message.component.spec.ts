import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormatMessageComponent } from './format-message.component';

describe('FormatMessageComponent', () => {
  let component: FormatMessageComponent;
  let fixture: ComponentFixture<FormatMessageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormatMessageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FormatMessageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
