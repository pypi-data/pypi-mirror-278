# SupaModel - Pydantic BaseModels and ORM for Supabase

`SupaModel` is a Python package that provides `pydantic` BaseModels and ORM for `Supabase`. It is built on top of [supabase-py](https://supabase.com/docs/reference/python/start) and [pydantic](https://pydantic-docs.helpmanual.io/).


I've been developing it within a monolithic FastAPI project, and I've decided to extract it into a separate package to make it easier to maintain and share with the community. Documents will come soon.


## Usage
Once completed, you will be able to use SupaModel to define your own models that map to tables in your Supabase database. You can then create, read, update, and delete records in your database using these models.

## Future Work
The project is still in its early stages, and there is a lot of work to be done. Future plans include adding more field types, relationships between models, and advanced query capabilities.


## Orms vs supabase-py vs SupaModel


You're absolutely right! Providing users with the flexibility to think about and interact with data in different ways is crucial for a robust and user-friendly library like supabase-py. Accommodating both composition-level thinking and aggregate/object-oriented thinking allows users to approach problems in a way that best suits their needs and preferences.

Here are a few ideas to help achieve this balance:

High-level table operations: Provide methods and classes that allow users to perform operations on entire tables, such as querying, filtering, sorting, and aggregating data. This enables users to think about data at a higher level and work with sets of records efficiently.

Object-oriented data access: Introduce an ORM-like layer that maps database tables to Python classes, allowing users to interact with data as objects. This provides a more intuitive and object-oriented approach to working with individual records, making it easier to retrieve, manipulate, and persist data.

Expression language support: Implement an expression language that allows users to construct complex queries and filters using a composable and expressive syntax. This gives users fine-grained control over their queries and enables them to leverage the full power of the underlying database.

Seamless integration: Ensure that the high-level table operations, object-oriented data access, and expression language can be used together seamlessly. Users should be able to switch between these approaches as needed, depending on the specific requirements of their task.

Clear documentation and examples: Provide comprehensive documentation and examples that demonstrate how to use supabase-py effectively in different scenarios. Highlight the strengths and use cases of each approach, helping users understand when to use high-level table operations, object-oriented data access, or the expression language.

Performance considerations: Optimize the library's performance for both high-level table operations and individual record access. Implement caching mechanisms, lazy loading, and efficient querying techniques to ensure that users can work with large datasets efficiently, regardless of their preferred approach.

By offering a balance between ORMs and expression language, supabase-py can cater to a wide range of user preferences and requirements. It allows users to think about data in a way that aligns with their mental models and problem-solving approaches, making the library more intuitive and enjoyable to use.

Remember to gather feedback from users and iterate on the design and implementation based on their experiences and needs. Continuously improving and refining supabase-py will help it become a valuable tool for developers working with Supabase and Python.



