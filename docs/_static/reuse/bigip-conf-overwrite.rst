What happened to my BIG-IP configuration changes?
`````````````````````````````````````````````````

If you make changes to objects in the partition managed by the |kctlr| -- whether via configuration sync or manually -- **the Controller will overwrite them**. By design, the |kctlr| keeps the BIG-IP system in sync with what it knows to be the desired configuration. For this reason, F5 does not recommend making any manual changes to objects in the partition(s) managed by the |kctlr|.
