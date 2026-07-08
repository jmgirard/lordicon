// Register the <lord-icon> custom element, wiring it to lottie-web's player.
// See https://element.lordicon.com/functions/index.defineElement.html
import lottie from 'lottie-web';
import { defineElement } from '@lordicon/element';

defineElement(lottie.loadAnimation);
