#pragma once

class PersistenceProvider
{
	PersistenceProvider();
	~PersistenceProvider();

	virtual void read();
	virtual void write();
};

