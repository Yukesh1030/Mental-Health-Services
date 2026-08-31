 = @(
    "admin-dashboard.html",
    "admin-clients.html",
    "admin-therapists.html",
    "admin-sessions.html",
    "admin-reports.html",
    "admin-alerts.html",
    "admin-settings.html"
)

 = '(?s)<div class="brand">.*?<div class="sidebar-footer".*?</div>'
 = '(?s)\.nav-item\{[^}]*\}'

foreach ( in ) {
    if (Test-Path ) {
         = Get-Content  -Raw
        
        # Add text-decoration:none to .nav-item CSS
         = ".nav-item{
    position:relative; z-index:1; display:flex; align-items:center; gap:12px;
    padding:11px 12px; border-radius:var(--radius-sm); color:var(--ink-soft); font-size:0.88rem; font-weight:500;
    cursor:pointer; transition:color .2s ease; background:transparent; border:none; text-align:left; width:100%;
    text-decoration: none;
  }"
         =  -replace , 

        # We will manually replace the sidebar HTML instead of regex because it's safer.
        Set-Content  -Value  -NoNewline
    }
}
