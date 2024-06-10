from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(
        cls, 
        v: str | ObjectId
    ):
        if isinstance(v, ObjectId):
            return v
        elif not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        '''Will throw ValueError if not set:

        ValueError: Value not declarable with JSON Schema,
            field: name='id' 
            type=PyObjectId 
            required=False 
            default_factory='<function PyObjectId>' 
            alias='_id'
        '''
        field_schema.update(type="string", example='63ee34b40fc20429fcb8dc1c')
