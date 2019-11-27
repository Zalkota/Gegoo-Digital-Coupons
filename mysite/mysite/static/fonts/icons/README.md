# Refactoring UI Icons

The easiest way to use these icons is as inline SVG elements:

```html
<a href="#">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon-mail">
    <path class="primary" d="M22 8.62V18a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8.62l9.55 4.77a1 1 0 0 0 .9 0L22 8.62z"/>
    <path class="secondary" d="M12 11.38l-10-5V6c0-1.1.9-2 2-2h16a2 2 0 0 1 2 2v.38l-10 5z"/>
  </svg>
  
  Contact Us
</a>
```

To change the color of an icon, provide your own CSS for the the `.primary` and `.secondary` classes, setting the `fill` attribute to your desired color:

```css
.primary {
  fill: #ffbbca;
}

.secondary {
  fill: #6f213f;
}
```

Since the icons are designed to be used as inline SVGs, you can easily customize these class names if needed by simply replacing the classes on the child elements of the parent `svg` element:

```diff
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon-mail">
-   <path class="primary"
+   <path class="rfui-icon-primary"
      d="M22 8.62V18a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8.62l9.55 4.77a1 1 0 0 0 .9 0L22 8.62z"
    />
-   <path class="secondary"
+   <path class="rfui-icon-secondary"
      d="M12 11.38l-10-5V6c0-1.1.9-2 2-2h16a2 2 0 0 1 2 2v.38l-10 5z"
    />
  </svg>
```

See the provided `demo.html` file for more examples of using the icons.
