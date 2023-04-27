
# Vlsir Language Bindings 

Language-specific bindings to the `vlsir` protobuf schemas.  
Language support breaks into three tiers: 

| Tier | Language(s)            | Support | 
| ---- | ---------------------- | ------- |
| 1    | Python, Rust           | Built-in    |
| 2    | C++, JavaScript, Julia | Recommended Recipe   |
| 3    | All others             | Community/ Schema Only |   

* Tier 1 *Built-In* Bindings are compiled by the VLSIR authors, and tracked here in the VLSIR source tree. They are also published to the relevant language-specific package managers, generally under the library/ package name `vlsir`. 
* Tier 2 *Recommended Recipes* are tested recipes for building bindings to the VLSIR schemas. While no official bindings are provided or published, compilation recipes are tested as part of VLSIR continuous integration. Recipes are generally provided as scripts in [vlsir/scripts/](../scripts/).
* Tier 3 *Community/ Schema Only* bindings are provided by the community, or are generated from the VLSIR schema files.
