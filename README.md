#### Before this patch `unsymlink-lib --analyze` output contains:
  
orphan dirs/files (not owned by any package) that will be moved to /usr/local/lib/:  
        perl5  
  
#### And with this patch `unsymlink-lib --analyze` output contains:
  
orphan dirs/files (not owned by any package) that will be kept in /usr/local/lib64/:  
        perl5  
  
#### This helps to preserve perl modules, installed manually or via CPAN (not to run manually 
`mv /usr/local/lib/perl5 /usr/local/lib64`  
#### after the migrating).
