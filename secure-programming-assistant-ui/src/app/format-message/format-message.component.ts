import { Component, Input } from '@angular/core';
import { Message } from '../../models/types';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';

@Component({
  selector: 'app-format-message',
  standalone: true,
  imports: [CommonModule, MarkdownModule],
  templateUrl: './format-message.component.html',
  styleUrl: './format-message.component.scss'
})
export class FormatMessageComponent {
  @Input() message: Message | undefined = undefined;
  @Input() showEntity: boolean = true;
}
